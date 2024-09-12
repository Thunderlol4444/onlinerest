import React, {useEffect} from 'react';
import {Button, Link, Text} from "@chakra-ui/react";
import {useNavigate} from "react-router-dom";

export default function Register() {
    const [registrationFailed, setRegistrationFailed] = React.useState(false);
    const [formData, setFormData] = React.useState({username:'', email:'', password:'', password2:''});
    const navigate = useNavigate();
    const [incorrectPassword, setPassword] = React.useState(false);
    const [disabled, setDisabled] = React.useState(true);
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prevState => ({...prevState, [name]: value,}));

        if (name === "password2" && formData.password !== value) {
            setPassword(true);
            console.log("Incorrect password");
        }else
        {
            setPassword(false);
        }
    }
    useEffect(() => {

        const isEmpty = Object.values(formData).some(value => value === '');
        setDisabled(isEmpty || incorrectPassword);

    }, [handleChange, incorrectPassword]);


    const handleSubmit = (e) => {
        e.preventDefault()
        const url = new URL("http://localhost:8000/register");
        url.searchParams.append("email", formData.email);
        url.searchParams.append("password", formData.password);
        url.searchParams.append("username", formData.username);
        fetch(url, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                setRegistrationFailed(false);
                navigate("/");
            } else {
                setRegistrationFailed(true);
                console.error("Login failed");
            }
        })
        .catch(error => {
            console.error("Error:", error)
            setRegistrationFailed(true);
        });
    };

    return (
        <div className="App">
            <div className="App-header"><Text fontWeight="bold" pb="5">NEW ACCOUNT</Text>
                <form id="register" onSubmit={handleSubmit} className="form-group">
                    <label htmlFor="name" className="label-block">Username:</label>
                    <input type="name" className="form-control" id="username" onChange={handleChange}
                           value={formData.username} name="username"/>
                    <br/>
                    <label htmlFor="email" className="label-block">Email address:</label>
                    <input type="email" className="form-control" id="email" onChange={handleChange}
                           value={formData.email} name="email"/>
                    <br/>
                    <label htmlFor="pwd" className="label-block">Password:</label>
                    <input type="password" className="form-control" id="password" onChange={handleChange}
                           value={formData.password} name="password"/>
                    <br/>
                    <label htmlFor="pwd" className="label-block">Re-enter password:</label>
                    <input type="password" className="form-control" id="pwd" onChange={handleChange}
                           value={formData.password2} name="password2"/>
                    {incorrectPassword === true && (
                        <Text color="red">*Incorrect password</Text>
                    )}
                </form>
                <Button colorScheme="blue" type="submit" form="register" size="sm" isDisabled={disabled}>Register</Button>
                {registrationFailed === true && (
                    <Text color="red" mt={2} fontSize="large">Registration failed. Please retry.</Text> // Conditionally render the retry message
                )}
                <Link href="/" color="teal.300" fontSize="medium" pt="3" textDecorationLine="underline">Back</Link>

            </div>
        </div>
    )
}