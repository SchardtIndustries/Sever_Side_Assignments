const express = require('express');
const app = express();
const port = 3000;

// Mock user data
const users = {
  '1': { id: '1', name: 'John Doe', products: ['1', '2'] },
  '2': { id: '2', name: 'Jane Smith', products: ['2'] }
};

app.get('/users/:id', (req, res) => {
  const user = users[req.params.id];
  if (!user) {
    return res.status(404).json({ message: 'User not found' });
  }
  res.json(user);
});

app.listen(port, () => {
  console.log(`User service running on port ${port}`);
});
