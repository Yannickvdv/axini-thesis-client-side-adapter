var express = require('express');
var router = express.Router();
const User = require('../models/user')

/* GET users listing. */
router.get('/', function(req, res, next) {
  User.all((err, user) => res.status(200).json(user));
});

router.post('/', (req, res) => {
  var newUser = req.body;
  User.add(newUser, (err, data) => {
    if(err) {
      res.status(400, 'The user could not be added').send();
    } else {
      res.status(201).send(data);
    }
  });
});


router.put('/:id', (req, res) => {
  var id = req.params.id;
  var updatedUser = JSON.parse(req.body);
  updatedUser.id = parseInt(id);
  User.update(updatedUser, (err, data) => {
    if(err) {
      res.status(404, 'The user is not found').send();
    } else {
      res.status(204).send(data);
    }}
  );
});

router.delete('/:id', (req, res) => {
  var id = parseInt(req.params.id);
  User.delete(id, (err) => {
    if(err) {
      res.status(404).send();
    } else {
      res.status(200).send();
    }
  });
});

module.exports = router;
