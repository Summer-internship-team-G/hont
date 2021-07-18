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
            const postVal = {
                id: account.id,
                password: account.pw,
            }
            await axios.post(postUrl, postVal)
            .then(function (response){
                setSuccess(response.data.success);
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
                history.replace("/");
            }
            else{
                alert("로그인에 실패하였습니다.");
            }
            
        }

        return {
            account,
            success,
            handleAccount,
            handleLogin,
        }
    }

    const { postUrl } = "/api/?";
    const history = useHistory();
    const { account, success, handleAccount, handleLogin } = useGetData();

    return(
        <>
            <div className="contents1">
                <form>
                    <label for="id">아이디 </label>
                    <input 
                        type="text" 
                        id="id" 
                        name="id" 
                        placeholder="아이디를 입력해주세요." 
                        required
                        onChange={handleAccount}
                    />
                    <p/>
                    <label for="password">비밀번호 </label>
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