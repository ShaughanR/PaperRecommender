import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const navigate = useNavigate();

    const handleLogin = async (event) => {
        event.preventDefault();

        setError("");

        try {
            const response = await fetch(
                "http://127.0.0.1:8003/api/auth/login",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        username: username,
                        password: password
                    })
                }
            );

            if (!response.ok) {
                setError("Incorrect username or password.");
                return;
            }

            const data = await response.json();

            localStorage.setItem(
                "access_token",
                data.access_token
            );

            navigate("/");
        }
        catch (error) {
            setError("Unable to connect to the server.");
        }
    };

    return (
        <div className="auth-page">

            <div className="auth-card">

                <h1>Login</h1>

                <form
                    className="auth-form"
                    onSubmit={handleLogin}
                >
                    <input
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={(event) => setUsername(event.target.value)}
                    />

                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(event) => setPassword(event.target.value)}
                    />

                    <button type="submit">
                        Login
                    </button>
                </form>

                {error && (
                    <p className="auth-error">
                        {error}
                    </p>
                )}

                <button
                    className="auth-secondary-button"
                    onClick={() => navigate("/register")}
                >
                    Create an Account
                </button>

            </div>

        </div>
    );
}

export default Login;