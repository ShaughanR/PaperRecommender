import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Register() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const navigate = useNavigate();

    const handleRegister = async (event) => {
        event.preventDefault();

        setError("");

        try {
            const response = await fetch(
                "http://127.0.0.1:8002/api/auth/register",
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
                const data = await response.json();

                setError(data.detail);
                return;
            }

            navigate("/login");
        }
        catch (error) {
            setError("Unable to connect to the server.");
        }
    };

    return (
        <div>
            <h1>Create Account</h1>

            <form onSubmit={handleRegister}>
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
                    Create Account
                </button>
            </form>

            {error && <p>{error}</p>}

            <button onClick={() => navigate("/login")}>
                Already have an account?
            </button>
        </div>
    );
}

export default Register;