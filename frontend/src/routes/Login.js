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

const Login = () => {
    const useGetData = () => {
        const [account, setAccount] = useState({
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
            const postUrl = "http://localhost:5000/auth/login";
            const postVal = {
                id: account.id,
                password: account.pw,
            }
            // console.log(postVal);
            await axios.post(postUrl, postVal, {
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then((response) => {
                if (response.data.status == "fail") {
                    alert(response.data.message);
                }
                else if (response.data.status == "success"){
                    localStorage.clear();
                    localStorage.setItem("token", response.data.auth_token);
                    localStorage.setItem("id", account.id);
                    
                    alert(response.data.message);
                    history.replace("/");
                }
            });
        }

        const handleLogin = (e) => {
            //새로고침 방지
            e.preventDefault();
            postData();
        }

        return {
            // account,
            // success,
            handleAccount,
            handleLogin,
        }
    }

    // const { setUser } = useUserContext();
    const history = useHistory();
    const { handleAccount, handleLogin } = useGetData();

    useEffect(() => {
        if (localStorage.getItem('token') !== null) {
            history.replace("/");
        } 
    }, []);

    return(
            <div className="contents1">
                <form className="textShadow2">
                    <Label htmlFor="id">아이디 </Label>
                    <Input 
                        type="text" 
                        id="id" 
                        name="id" 
                        placeholder="아이디를 입력해주세요." 
                        required
                        onChange={handleAccount}
                    />
                    <p/>
                    <Label htmlFor="password">비밀번호 </Label>
                    <Input 
                        type="password"
                        id="pw"
                        name="pw"
                        placeholder="비밀번호를 입력해주세요." 
                        required
                        onChange={handleAccount}
                    />
                    <p/>
                    <button className="lightest bigBtn boxShadow" type="reset">초기화</button>
                    <button className="neutral bigBtn boxShadow" type="button" onClick={handleLogin}>로그인</button>
                </form>
            </div>
    )
}

export default Login;