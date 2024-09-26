import React, {useEffect, useState} from 'react';
import {Button, Link, Text} from "@chakra-ui/react";
import {useNavigate} from "react-router-dom";

export default function ChangePassword() {
    const [formData, setFormData] = useState({password:"",password2:""})
    const [disabled, setDisabled] = React.useState(true);
    const [incorrectPassword, setPassword] = React.useState(false);
    const [passwordChanged, setPasswordChanged] = React.useState(false);
    const [changeFailed, setChangeFailed] = React.useState(false);
    const [msg, setMsg] = React.useState("");
    const navigate = useNavigate();
    const [emailVerify, setEmailVerify] = React.useState(false);
    const [verificationFailed, setVerificationFailed] = React.useState(false);
    const [OTP, setOTP] = React.useState({OTP:'', inputOTP:""});

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

   const handleChange2 = (e) => {
        const { name, value } = e.target;
        setOTP(prevState => ({...prevState, [name]: value,}));
        setEmailVerify(false);
    }

    const handleSubmit = (e) => {
        e.preventDefault()
        const url = new URL("https://onlinerest-1022384984816.asia-southeast1.run.app/email_verification");
        url.searchParams.append("email", formData.email);
        url.searchParams.append("name", formData.username)
        fetch(url, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
        }).then((response) => response.json())
            .then(data => {
                if (data.OTP){
                    setOTP({OTP:data.OTP});
                    setEmailVerify(true);
                }else{
                    setEmailVerify(false);
                }
            })
        .catch(error => {
                console.error("Error:", error)
            });
    }

    const handleSubmit2 = async (e) => {
        e.preventDefault()
        if (OTP.OTP===OTP.inputOTP){
            console.log(formData)
            const url = new URL("https://onlinerest-1022384984816.asia-southeast1.run.app/change-password");
            url.searchParams.append("email", formData.email);
            url.searchParams.append("new_password", formData.password)
            await fetch(url, {
                method: "POST",
                headers: {"Content-Type": "application/json"},
            }).then((response) => response.json())
                .then(data => {
                    if (data.message) {
                        setPasswordChanged(true)
                        const timer = setTimeout(() => {
                            navigate("/");
                        }, 3000);
                        return () => clearTimeout(timer);
                    } else {
                        setMsg(data.detail)
                        setPasswordChanged(false)
                        setChangeFailed(true)
                    }
                })
            .catch(error => {
                console.error("Error:", error)
                setVerificationFailed(true);
            });
        }else{
            setVerificationFailed(true)
        }

    };

    useEffect(() => {

        const isEmpty = Object.values(formData).some(value => value === '');
        setDisabled(isEmpty || incorrectPassword);
        // const referrer = document.referrer;
        // console.log("Referrer: ",referrer);

    }, [handleChange, incorrectPassword]);
    if (emailVerify === false){
        return (
            <div className="form-change-password"><Text color="white" fontSize="xx-large" fontWeight="bold"
                                                        pb="5">Reset Password</Text>
                <form id="change_password" onSubmit={handleSubmit} className="form-group">
                    <label htmlFor="name" className="label-block">Username:</label>
                    <input type="name" className="form-control" id="username" onChange={handleChange}
                           value={formData.username} name="username" autoComplete='off'/>
                    <br />
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
                <Button colorScheme="blue" type="submit" form="change_password" size="sm"
                        isDisabled={disabled}>Change password</Button>
                <Link href="/" color="teal.300" fontSize="medium" pt="3" textDecorationLine="underline">Back</Link>
            </div>
        )
    } else {
        return (
            <div className="App">
                <div className="App-header"><Text fontWeight="bold" pb="5" flexWrap="wrap">Verification code</Text>
                    <form id='verify' onSubmit={handleSubmit2} className="form-group" spellCheck="false">
                        <div className="pinBox">
                            <input type="text" maxLength="4" id="verification_code" autoComplete='off' name="inputOTP"
                                   value={OTP.inputOTP} onChange={handleChange2}/>
                        </div>
                    </form>
                    {verificationFailed === true && (
                        <Text color="red" mb={2} fontSize="large">Validation failed. Please retry.</Text> // Conditionally render the retry message
                    )}
                    {passwordChanged === true && (
                        <Text color="green" mb={2} fontSize="large">Password changed. Redirect to login</Text> // Conditionally render the retry message
                    )}
                    {changeFailed === true && (
                    <Text color="red" mt={2} fontSize="large">Change password failed. {msg}</Text> // Conditionally render the retry message
                    )}
                    <Button colorScheme="green" type="submit" form="verify" size="sm" mb="5">Verify</Button>
                    <Button colorScheme="blue" type="submit" form="register" size="sm" bottom='390px' right='47%'
                            onClick={() => setEmailVerify(false)}>Back</Button>
                </div>
            </div>
        )
    }
}