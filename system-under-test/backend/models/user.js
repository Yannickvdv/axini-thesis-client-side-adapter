const sqlite3 = require('sqlite3');
const db = new sqlite3.Database(':memory:');

db.serialize(() => {
  const sql = 'CREATE TABLE IF NOT EXISTS user (id integer primary key, name)';
  db.run(sql);
  db.run('INSERT INTO user(name) VALUES(?)', 'bart');
  db.run('INSERT INTO user(name) VALUES(?)', 'dirk');
  db.run('INSERT INTO user(name) VALUES(?)', 'henk');
});

class User {
  constructor(id, name){
    this.id = id;
    this.name = name;
  }

  static all(callback){
    db.all('SELECT * FROM user', callback);
  };

  static add(user, callback){
    const sql = 'INSERT INTO user(name) VALUES(?)';
    db.run(sql, user.name, callback);
  };

  static update(user, callback){
    console.log(user);
    const sql = 'UPDATE user SET name = ? WHERE id = ?';
    db.run(sql, user.name, user.id, callback);
  };

  static delete(id, callback){
    const sql = 'DELETE FROM user where id = ?';
    db.run(sql, id, callback);
  };
}

module.exports = User;
