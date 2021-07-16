import React, { useState } from "react";
// import { Link } from "react-router-dom";
import SVG from "../components/SVG";
import axios from "axios";
import { useHistory } from "react-router-dom";
import styled from "styled-components";
// import useUserContext from "../components/user-context";

const Input = styled.input`
    border: 1px solid black;
    border-radius: 0px;
    height: 50px;
    width: 400px;
    margin-top: 10px;
    text-align: center;
    font-size: 18px;
`;

const Label = styled.label`
    position: relative;
    top: 10px;
    font-family: "Coda";
    font-size: 36px;
    font-weight: 600;
`;

const Login = () => {
    const useGetData = () => {
        const [account, setAccount] = useState({
            id: "",
            pw: "",
        });
        const [success, setSuccess] = useState(false);

        const handleAccount = (e) => {
            setAccount({
                ...account,
                [e.target.name]: e.target.value,
            });
        }
        
        const postData = async () => {
            const postVal = {
                id: account.id,
                password: account.pw,
            }
            // return await axios.post(postUrl, postVal);
            await axios.post(postUrl, postVal)
            .then(function (response){
                setSuccess(response);
            })
            .catch(function (error){
                console.log(error);
            })
        }

        const handleLogin = (e) => {
            //새로고침 방지
            e.preventDefault();
            postData();
            if (success) {
                // setUser(account);
                history.replace("/");
                // history.push({
                //     pathname: "/Home";
                //     state: {

                //     }
                // })
            }
            else{
                alert('로그인 실패');
            }
            
        }

        return {
            account,
            success,
            handleAccount,
            handleLogin,
        }
    }

    // const { setUser } = useUserContext();
    const { postUrl } = "/api/?";
    const history = useHistory();
    const { account, success, handleAccount, handleLogin } = useGetData();

    return(
        <>
            <div className="contents1">
                <form>
                    <Label>아이디 </Label>
                    <Input 
                        type="text" 
                        id="id" 
                        name="id" 
                        placeholder="아이디를 입력해주세요." 
                        required size="17" 
                        onChange={handleAccount}
                    />
                    <p/>
                    <Label>비밀번호 </Label>
                    <Input 
                        type="password"
                        id="pw"
                        name="pw"
                        placeholder="비밀번호를 입력해주세요." 
                        required size="10" 
                        onChange={handleAccount}
                    />
                    <p/>
                    <button className="lightest bigBtn" type="reset">초기화</button>
                    <button className="neutral bigBtn" type="button" onClick={handleLogin}>로그인</button>
                </form>
            </div>
        </>   
    )
}

export default Login;