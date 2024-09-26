import React, {useEffect} from "react";
import "../App.css"
import {useNavigate} from "react-router-dom";
import {Box, Text, Collapse, Fade} from "@chakra-ui/react";

export default function Logout() {
    const navigate = useNavigate();
    const [output, setOutput] = React.useState(null);
    const [fade, setFade] = React.useState(true);

    useEffect(() => {
        const performLogout = async () => {
            try {
                const response = await fetch("https://onlinerest-1022384984816.asia-southeast1.run.app/logout", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
                    },
                });
                let result = await response.json();
                setOutput(result.message);

                if (!response.ok) {
                    throw new Error("Logout failed");
                }
            } catch (error) {
                console.error("Logout error", error);
                localStorage.removeItem("access_token")
            }

            // Redirect to the login page after 3 seconds
            const timer = setTimeout(() => {
                navigate("/");
            }, 3000);
            return () => clearTimeout(timer);
        };
        performLogout();
    }, [navigate]);
    console.log("Output: " + output);
    setTimeout(()=> {
        setFade(prevState => !prevState)
    },1500);

    return (
        <div className="App-header">
            <Fade in={true}>
                <Collapse in={fade} animateOpacity>
                    <Box textAlign="center" color="white" fontWeight="700" bg="white" p="15px" borderRadius="10">
                        <Text fontSize="2xl" color="green.700">Logged out</Text>
                    </Box>
                </Collapse>
            </Fade>
        </div>
    )
}
