module.exports = {
    "env": {
        "node": true
    },
    "extends": "eslint:recommended",
    "rules": {
        "no-console": 0,
        "no-unused-vars": ["error", {"args": "none"}],
        "indent": [2, 2, {
            "SwitchCase": 1
        }],
        "linebreak-style": [
            "error",
            "unix"
        ],
        "quotes": [
            1,
            "single"
        ],
        "semi": [
            "error",
            "always"
        ]
    },
    "parserOptions": {
        "ecmaVersion": 6,
        "ecmaFeatures": {
            "experimentalObjectRestSpread": true
        }
    }
};