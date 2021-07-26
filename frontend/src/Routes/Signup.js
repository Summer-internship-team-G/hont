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
        // const [duplicate, setDuplicate] = useState(false);
        // const [clickDuplicateBtn, setClickDuplicateBtn] = useState(false);
        // const [success, setSuccess] = useState(false);

        const handleAccount = (e) => {
            setAccount({
                ...account,
                [e.target.name]: e.target.value,
            });
        }
        // const duplicateCheck = async () => {
        //     const postVal = {
        //         id: account.id,
        //     }
        //     await axios.post(postUrl, postVal)
        //     .then(function (response){
        //         // 중복된 아이디가 존재할 경우
        //         if(response.data.duplicate){
        //             setDuplicate(true);
        //             setClickDuplicateBtn(true);
        //         }
        //         // 중복된 아이디가 없을 경우
        //         else{
        //             setDuplicate(false);
        //             setClickDuplicateBtn(false);

        //         }
        //     })
        //     .catch(function (error){
        //         console.log(error);
        //     })
        // }
        
        // const handleDuplicate = (e) => {
        //     e.preventDefault();
        //     duplicateCheck();
        // }
 
        
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
                    // setSuccess(true);
                    localStorage.clear();
                    // localStorage.setItem("token", response.data.auth_token);
                    alert(response.data.message);
                    history.replace("/login");
                }
                else if (response.data.status == "fail"){
                    alert(response.data.message);
                }
            });
        }

        // const postData = async () => {
        //     const postVal = {
        //         name: account.name,
        //         id: account.id,
        //         password: account.pw,
        //     }
        //     await axios.post(postUrl, postVal)
        //     .then(function (response){
        //         setSuccess(true);
        //     })
        //     .catch(function (error){
        //         alert(error);
        //     })
        // }

        const handleSignup = (e) => {
            e.preventDefault();
            postData();
            // if (success) {
            //     history.replace("/login");
            // }
            // else{
            //     alert("회원가입에 실패하였습니다.");
            // }
        }

        return {
            // duplicate,
            handleAccount,
            // handleDuplicate,
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
                <Label htmlFor="name">이름 </Label>
                <Input 
                    type="text" 
                    id="name" 
                    name="name" 
                    placeholder="이름을 입력해주세요." 
                    required
                    onChange={handleAccount}
                />
                <p/>
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
                <button className="darkest bigBtn boxShadow" type="button" onClick={handleSignup}>회원가입</button>
            </form>
        </div>
    )
}

export default Signup;