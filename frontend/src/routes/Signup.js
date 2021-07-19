import React, { useState } from "react";
import axios from "axios";
import { useHistory } from "react-router-dom";

const Signup = () => {
    const useGetData = () => {
        const [account, setAccount] = useState({
            name: "",
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
            const postUrl = "http://localhost:5000/user/signup";
            const postVal = {
                name: account.name,
                id: account.id,
                password: account.pw,
            }
            console.log(postVal);
            await axios.post(postUrl, postVal)
            .then((response) => {
                if (response.data.error == "true") {
                    console.log("회원가입에 실패하였습니다.");
                }
                else {
                    setSuccess(true);
                    history.replace("/login");
                }
            });
        }

        const handleSignup = (e) => {
            e.preventDefault();
            postData();
        }

        return {
            account,
            success,
            handleAccount,
            handleSignup,
        }
    }

    const history = useHistory();
    const { account, success, handleAccount, handleSignup } = useGetData();

    return(
        <div className="contents1">
            <form>
                <label htmlFor="name">이름 </label>
                <input 
                    type="text" 
                    id="name" 
                    name="name" 
                    placeholder="이름을 입력해주세요." 
                    required
                    onChange={handleAccount}
                />
                <p/>
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
                <button className="darkest bigBtn" type="button" onClick={handleSignup}>회원가입</button>
            </form>
        </div>
    )
}

export default Signup;