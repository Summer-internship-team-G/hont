import React, { useState, useEffect } from "react";
import axios from "axios";
import { useHistory } from "react-router-dom";
import styled from "styled-components";

const Input = styled.input`
    border: 1px solid black;
    border-radius: 0px;
    height: 50px;
    width: 400px;
    margin-top: 10px;
    text-align: center;
    font-size: 18px;
    display: inline-block;
`;

const Label = styled.label`
    position: relative;
    top: 10px;
    font-family: "Coda";
    font-size: 36px;
    font-weight: 600;
    width: 200px;
    display: inline-block;
    text-align: left;
`;

const Signup = () => {
    const useGetData = () => {
        const [account, setAccount] = useState({
            name: "",
            id: "",
            pw: "",
        });

        const handleAccount = (e) => {
            setAccount({
                ...account,
                [e.target.name]: e.target.value,
            });
        }
        
        const postData = async () => {
            const postUrl = "http://localhost:5000/auth/register";
            const postVal = {
                name: account.name,
                id: account.id,
                password: account.pw,
            }
            await axios.post(postUrl, postVal, {
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then((response) => {
                if (response.data.status == "success") {
                    localStorage.clear();
                    localStorage.setItem("token", response.data.auth_token);
                    alert(response.data.message);
                    history.replace("/login");
                }
                else if (response.data.status == "fail"){
                    alert(response.data.message);
                }
            });
        }

        const handleSignup = (e) => {
            e.preventDefault();
            postData();
        }

        return {
            handleAccount,
            handleSignup,
        }
    }


    const history = useHistory();
    const { handleAccount, handleSignup } = useGetData();

    useEffect(() => {
        if (localStorage.getItem('token') !== null) {
            history.replace("/");
        } 
    }, []);

    return(
        <div className="contents1">
            <form className="textShadow2">
                <Label htmlFor="name">?????? </Label>
                <Input 
                    type="text" 
                    id="name" 
                    name="name" 
                    placeholder="????????? ??????????????????." 
                    required
                    onChange={handleAccount}
                />
                <p/>
                <Label htmlFor="id">????????? </Label>
                <Input 
                    type="text" 
                    id="id" 
                    name="id" 
                    placeholder="???????????? ??????????????????." 
                    required
                    onChange={handleAccount}
                />
                <p/>
                <Label htmlFor="password">???????????? </Label>
                <Input 
                    type="password"
                    id="pw"
                    name="pw"
                    placeholder="??????????????? ??????????????????." 
                    required 
                    onChange={handleAccount}
                />
                <p/>
                <button className="lightest bigBtn boxShadow" type="reset">?????????</button>
                <button className="darkest bigBtn boxShadow" type="button" onClick={handleSignup}>????????????</button>
            </form>
        </div>
    )
}

export default Signup;