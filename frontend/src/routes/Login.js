import React, { useState } from "react";
import axios from "axios";
import { useHistory } from "react-router-dom";

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
            const postUrl = "http://localhost:5000/user/login";
            const postVal = {
                id: account.id,
                password: account.pw,
            }
            await axios.post(postUrl, postVal)
            .then((response) => {
                if (response.data.error == "true") {
                    console.log("로그인에 실패하였습니다.");
                }
                else {
                    setSuccess(true);
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
            account,
            success,
            handleAccount,
            handleLogin,
        }
    }

    const history = useHistory();
    const { account, success, handleAccount, handleLogin } = useGetData();

    return(
        <>
            <div className="contents1">
                <form>
                    <label htmlFor="id">아이디 </label>
                    <input 
                        type="text" 
                        id="id" 
                        name="id" 
                        placeholder="아이디를 입력해주세요." 
                        required
                        onChange={handleAccount}
                    />
                    <p/>
                    <label htmlFor="password">비밀번호 </label>
                    <input 
                        type="password"
                        id="pw"
                        name="pw"
                        placeholder="비밀번호를 입력해주세요." 
                        required
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