import React, {useEffect} from 'react';
import {Button, Link, Text} from "@chakra-ui/react";
import {useNavigate} from "react-router-dom";

export default function Register() {
    const [registrationFailed, setRegistrationFailed] = React.useState(false);
    const [registrationSuccess, setRegistrationSuccess] = React.useState(false);
    const [formData, setFormData] = React.useState({username:'', email:'', password:'', password2:''});
    const navigate = useNavigate();
    const [incorrectPassword, setPassword] = React.useState(false);
    const [disabled, setDisabled] = React.useState(true);
    const [emailVerify, setEmailVerify] = React.useState(false);
    const [verificationFailed, setVerificationFailed] = React.useState(false);
    const [OTP, setOTP] = React.useState({OTP:'', inputOTP:""});
    const [msg, setmsg] = React.useState("");

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prevState => ({...prevState, [name]: value,}));
        setRegistrationFailed(false)
        if (name === "password2" && formData.password !== value) {
            setPassword(true);
            console.log("Incorrect password");
        }else
        {
            setPassword(false);
        }
    }

   const handleChange2 = (e) => {
        const { name, value } = e.target;
        setOTP(prevState => ({...prevState, [name]: value,}));
    }

    const handleSubmit = (e) => {
        e.preventDefault()
        const url = new URL("http://localhost:8000/register/email_verification");
        url.searchParams.append("email", formData.email);
        url.searchParams.append("name", formData.username)
        fetch(url, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
        }).then((response) => response.json())
            .then(data => {
                if (data.OTP){
                    setOTP({OTP: data.OTP,})
                    setEmailVerify(true);
                }else{
                    setEmailVerify(false);
                    setRegistrationFailed(true);
                }
            })
    }

    const handleSubmit2 = (e) => {
        e.preventDefault()
        if (OTP.OTP===OTP.inputOTP){
            console.log(formData)
            const url = new URL("http://localhost:8000/register");
            url.searchParams.append("username", formData.username);
            url.searchParams.append("email", formData.email);
            url.searchParams.append("password", formData.password);
            fetch(url, {
                method: "POST",
                headers: {"Content-Type": "application/json"},
            })
            .then(response => response.json())
            .then(data => {
                setmsg(data)
                if (data.message) {
                    setRegistrationSuccess(true)
                    const timer = setTimeout(() => {
                          navigate("/");
                          setRegistrationSuccess(false)
                          }, 3000);
                    return () => clearTimeout(timer);
                } else {
                    setRegistrationFailed(true);
                    console.error("Login failed");
                }
            })
            .catch(error => {
                console.error("Error:", error)
                setRegistrationFailed(true);
            });
        }else{
            setVerificationFailed(true)
        }

    };

    useEffect(() => {

        const isEmpty = Object.values(formData).some(value => value === '');
        setDisabled(isEmpty || incorrectPassword);

    }, [handleChange, incorrectPassword, handleSubmit, emailVerify, registrationFailed]);

    if (emailVerify === false){
        return (
            <div className="App">
                <div className="App-header"><Text fontWeight="bold" pb="5">NEW ACCOUNT</Text>
                    <form id="register" onSubmit={handleSubmit} className="form-group">
                        <label htmlFor="name" className="label-block" >Username:</label>
                        <input type="name" className="form-control" id="username" onChange={handleChange}
                               value={formData.username} name="username" autoComplete='off'/>
                        <br/>
                        <label htmlFor="email" className="label-block">Email address:</label>
                        <input type="email" className="form-control" id="email" onChange={handleChange}
                               value={formData.email} name="email" autoComplete='off'/>
                        <br/>
                        <label htmlFor="pwd" className="label-block">Password:</label>
                        <input type="password" className="form-control" id="password" onChange={handleChange}
                               value={formData.password} name="password" autoComplete='off'/>
                        <br/>
                        <label htmlFor="pwd" className="label-block">Re-enter password:</label>
                        <input type="password" className="form-control" id="pwd" onChange={handleChange}
                               value={formData.password2} name="password2" autoComplete='off'/>
                        {incorrectPassword === true && (
                            <Text color="red">*Incorrect password</Text>
                        )}
                    </form>
                    <Button colorScheme="blue" type="submit" form="register" size="sm"
                            isDisabled={disabled}>Register</Button>
                    {registrationFailed === true && (
                        <Text color="red" mt={2} fontSize="large">Registration failed. Please retry.</Text> // Conditionally render the retry message
                    )}
                    <Link href="/" color="teal.300" fontSize="medium" pt="3" textDecorationLine="underline">Back</Link>

                </div>
            </div>
        )
    }else{
        return (
            <div className="App">
                <div className="App-header"><Text fontWeight="bold" pb="5" flexWrap="wrap">Verification code</Text>
                    <form id='verify' onSubmit={handleSubmit2} className="form-group" spellCheck="false">
                        <div className="pinBox">
                            <input type="text" maxLength="4" id="verification_code" autoComplete='off' name="inputOTP" value={OTP.inputOTP} onChange={handleChange2} />
                        </div>
                    </form>
                    {verificationFailed === true && (
                        <Text color="red" mb={2} fontSize="large">Validation failed. Please retry.</Text> // Conditionally render the retry message
                    )}
                    {registrationFailed === true && (
                        <Text color="red" mb={2} fontSize="large">{msg.detail}</Text> // Conditionally render the retry message
                    )}
                    {registrationSuccess === true && (
                        <Text color="green" mb={2} fontSize="large">Registration successful. Redirect to login</Text> // Conditionally render the retry message
                    )}
                    <Button colorScheme="green" type="submit" form="verify" size="sm" mb="5">Verify</Button>
                    <Button colorScheme="blue" type="submit" form="register" size="sm" bottom='390px' right='47%'
                            onClick={() => setEmailVerify(false)}>Back</Button>
                </div>
            </div>
        )
    }
}