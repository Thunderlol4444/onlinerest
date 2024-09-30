import React from "react";
import "../App.css"
import {
    Button,
    Text,
    Link,
} from "@chakra-ui/react";
import {useNavigate} from "react-router-dom";
import {access_token_context} from "../App";


export default function Login() {
    const [formData, setFormData] = React.useState({email:'', password:''})
    const {access_token, setToken } = React.useContext(access_token_context);
    const [loginFailed, setLoginFailed] = React.useState(false);
    const navigate = useNavigate();
    const [msg, setMsg] = React.useState('');


    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prevState => ({...prevState, [name]: value,}));
    };

    const handleSubmit = (e) => {
        e.preventDefault()
        const url = new URL("https://onlinerest-1022384984816.asia-southeast1.run.app/login");
        url.searchParams.append("email", formData.email);
        url.searchParams.append("password", formData.password);
        fetch(url, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            //body: JSON.stringify(newLogin)
        })
        .then(response => response.json())
        .then(data => {
            if (data.access_token) {
                setToken(data.access_token);
                localStorage.setItem("access_token", data.access_token); // Save the token in localStorage
                setLoginFailed(false);
                navigate("/landing"); // Navigate to the landing page
            } else {
                setLoginFailed(true);
                setMsg(data.detail);
                console.error("Login failed");
            }
        })
        .catch(error => {
            console.error("Error:", error)
            setLoginFailed(true);
        });
    };


    return (
        <div className="App">
            <div className="App-header"><Text fontWeight="bold" pb="5">LOGIN</Text>
                <form id="login" onSubmit={handleSubmit} className="form-group">
                    <label htmlFor="email" className="label-block">Email address:</label>
                    <input type="email" className="form-control" id="email" onChange={handleChange} value={formData.email} name="email"/>
                    <br/>
                    <label htmlFor="pwd" className="label-block">Password:</label>
                    <input type="password" className="form-control" id="pwd" onChange={handleChange} value={formData.password} name="password"/>
                </form>
                <Button colorScheme="blue" type="submit" form="login" size="sm">Submit</Button>
                <a href="/change-password" className="forget-button">Forget password?</a>
                {loginFailed===true && (
                    <Text color="red" mt={4}>{msg}. Please retry.</Text> // Conditionally render the retry message
                )}
                <Text pt="5" fontSize="medium">New Account?<Link href="/register" color="teal.300" fontSize="medium" pt="5" > Register</Link>
                </Text>

            </div>
        </div>
    )
}


