const express = require('express')
const app = express()
const mysql = require("mysql2")
const urlencodedParser = express.urlencoded({extended: false})
const jsonParser = express.json()


const conn = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    database: 'myDataBase',
    password: 'root'
}).promise()

app.use(express.static(__dirname + '/static'))

app.get('/login', (req, res) => {
    res.sendFile(__dirname + '/html/login.html')
})

app.post('/login', urlencodedParser, (req, res) => {
    if (!req.body) return res.sendStatus(400)
    let username = req.body.username
    let password = req.body.password
    if (username === 'admin' && password === '1234') {
        res.redirect('/admin-page')
    }
    else res.send('<h1>Уходи</h1>')
})

app.get('/admin-page', (req, res) => {
    res.sendFile(__dirname + '/html/admin-page.html')
})

app.post('/admin-page', jsonParser, (req, res) => {
    if (!req.body.user_id) {
        conn.query('SELECT * FROM users')
            .then(result => {
                res.json(result[0])
            })
            .catch(err => {
                console.log(err)
            })
    }
    else {
        user_id = req.body.user_id
        new_state = req.body.new_state
        conn.query('UPDATE users SET state = ? WHERE id = ?', [new_state, user_id])
            .then(() => {
                conn.query('SELECT * FROM users')
                    .then(result => {
                        res.json(result[0])
                    })
                    .catch(err => {
                        console.log(err)
                    })
            })
            .catch(err => {
                console.log(err)
            })
    }
})


app.listen('3000', () => console.log('Сервер запущен...'))
