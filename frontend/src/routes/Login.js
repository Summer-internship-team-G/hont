import React, { useState } from "react";
import axios from "axios";
import { useHistory } from "react-router-dom";

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
            handleAccount,
            handleLogin,
        }
    }

    const history = useHistory();
    const {  handleAccount, handleLogin } = useGetData();

    useEffect(() => {
        if (localStorage.getItem('token') !== null) {
            history.replace("/");
        } 
    }, []);

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