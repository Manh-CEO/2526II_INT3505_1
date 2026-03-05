const express = require('express');
const app = express();
const port = 3000;

app.use(express.json());

let users = [
    { id: 1, name: "Manh", age: 21, email: "[EMAIL_ADDRESS]" }
];

const handlers = {
    getAllUsers: (req, res) => {
        res.json(users);
    },

    getUser: (req, res) => {
        const user = users.find(u => u.id === parseInt(req.params.id));
        if (!user) return res.status(404).send("Không tìm thấy user");
        res.json(user);
    },

    createUser: (req, res) => {
        const { name, age, email } = req.body;
        const newUser = {
            id: Math.floor(Math.random() * 1000),
            name,
            age,
            email
        };
        users.push(newUser);
        res.status(201).json(newUser);
    },

    updateUser: (req, res) => {
        const user = users.find(u => u.id === parseInt(req.params.id));
        if (!user) return res.status(404).send("Không tìm thấy user");

        Object.assign(user, req.body);
        res.json(user);
    },

    deleteUser: (req, res) => {
        const initialLength = users.length;
        users = users.filter(u => u.id !== parseInt(req.params.id));

        if (users.length === initialLength) return res.status(404).send("Không tìm thấy user");
        res.send(`Đã xóa user ${req.params.id}`);
    }
};

const apis = [
    { name: "createUser", path: "/users", method: "POST", description: "Create a new user" },
    { name: "getUser", path: "/users/:id", method: "GET", description: "Get a user by id" },
    { name: "updateUser", path: "/users/:id", method: "PUT", description: "Update a user by id" },
    { name: "deleteUser", path: "/users/:id", method: "DELETE", description: "Delete a user by id" },
    { name: "getAllUsers", path: "/users", method: "GET", description: "Get all users" }
];

// Router register
for (const api of apis) {
    const handler = handlers[api.name];
    if (handler) {
        app[api.method.toLowerCase()](api.path, handler);
    } else {
        app[api.method.toLowerCase()](api.path, (req, res) => res.send(api.description));
    }
}

app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});