const express = require("express");
const basicAuth = require("basic-auth");
const jwt = require("jsonwebtoken");
const rateLimit = require("express-rate-limit");
const NodeCache = require("node-cache");

const app = express();
app.use(express.json());

const port = 3002;
const jwtSecret = "super-secret-key"; // for class only; use env var in real apps

// --- Rate limiting (advanced)
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  standardHeaders: true,
  legacyHeaders: false,
});
app.use(limiter);

// --- Cache (advanced)
const cache = new NodeCache({ stdTTL: 60 });

// --- Basic Auth helpers
function authenticate(username, password) {
  return username === "admin" && password === "password";
}

function basicAuthMiddleware(req, res, next) {
  const creds = basicAuth(req);

  if (!creds || !authenticate(creds.name, creds.pass)) {
    res.set("WWW-Authenticate", 'Basic realm="Authorization Required"');
    return res.sendStatus(401);
  }
  next();
}

// --- JWT middleware
function jwtAuthMiddleware(req, res, next) {
  const token = req.headers.authorization?.split(" ")[1];
  if (!token) return res.sendStatus(401);

  try {
    req.user = jwt.verify(token, jwtSecret);
    next();
  } catch (err) {
    return res.sendStatus(401);
  }
}

// --- ROUTING: Users (protected with Basic Auth)
app.get("/api/v1/users/:id", basicAuthMiddleware, async (req, res) => {
  try {
    const r = await fetch(`http://localhost:3000/users/${req.params.id}`);
    const data = await r.json();
    res.status(r.status).json(data);
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: "Gateway error contacting user-service" });
  }
});

// --- ROUTING: Products (protected with JWT)
app.get("/api/v1/products/:id", jwtAuthMiddleware, async (req, res) => {
  const id = req.params.id;

  // cache layer
  const cached = cache.get(`product:${id}`);
  if (cached) {
    console.log("Serving product from cache");
    return res.json(cached);
  }

  try {
    const r = await fetch(`http://localhost:3001/products/${id}`);
    const data = await r.json();
    cache.set(`product:${id}`, data);
    res.status(r.status).json(data);
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: "Gateway error contacting product-service" });
  }
});

// --- COMPOSITION: User + Products
app.get("/api/v1/userProducts/:userId", async (req, res) => {
  try {
    const userRes = await fetch(`http://localhost:3000/users/${req.params.userId}`);
    const user = await userRes.json();

    if (!userRes.ok) {
      return res.status(userRes.status).json(user);
    }

    const productIds = user.products || [];
    const products = await Promise.all(
      productIds.map((pid) =>
        fetch(`http://localhost:3001/products/${pid}`).then((r) => r.json())
      )
    );

    res.json({ user, products });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: "Error composing user + products" });
  }
});

// --- JWT issuance endpoint (optional part)
app.post("/auth", (req, res) => {
  const { username, password } = req.body || {};
  if (!authenticate(username, password)) {
    return res.status(401).json({ message: "invalid credentials" });
  }

  const token = jwt.sign({ username }, jwtSecret, { expiresIn: "1h" });
  res.json({ token });
});

app.listen(port, () => {
  console.log(`API Gateway running on port ${port}`);
});
