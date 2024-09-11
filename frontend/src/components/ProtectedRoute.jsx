import React, { useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { access_token_context } from "../App";
import { Box, Text } from "@chakra-ui/react";

const ProtectedRoute = ({ children }) => {
    const { access_token, setToken } = useContext(access_token_context);
    const navigate = useNavigate();
    useEffect(() => {
        const token = localStorage.getItem("access_token");
        if (token) {
            setToken(token);
        }
    if (!access_token) {
        // Redirect to the login page after 3 seconds
        const timer = setTimeout(() => {
            navigate("/");
        }, 3000);

        // Cleanup the timeout if the component is unmounted
        return () => clearTimeout(timer);
    }
    }, [access_token, navigate]);

    if (!access_token) {
        // If the user is not logged in, redirect to the login page
        // const delay = async() => {
        //     await delay(3000);
        //     return <Navigate to="/" replace />
        // }
        return (
            <>
                <Box textAlign="center" mt="50px">
                    <Text fontSize="2xl" color="red">Access blocked. Please login.</Text>
                </Box>
            </>);
    }

    // If the user is logged in, render the requested page
    return children;
};

export default ProtectedRoute;