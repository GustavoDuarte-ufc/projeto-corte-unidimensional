import {
    createContext,
    useEffect,
    useState
} from "react";

import * as authService
    from "../services/authService";

import {
    saveTokens,
    getAccessToken,
    getRefreshToken,
    removeTokens
} from "../services/tokenService";

export const AuthContext =
    createContext();

export function AuthProvider(
    {children}
){

    const [user,setUser] =
        useState(null);

    const [authenticated,
        setAuthenticated] =
        useState(false);

    const [loading,
        setLoading] =
        useState(true);

    async function signIn(
        credentials
    ){

        const data =
            await authService.login(
                credentials
            );

        saveTokens(
            data.access_token,
            data.refresh_token
        );

        await loadUser();
    }

    async function loadUser(){

        try{

            const user =
                await authService.me();

            setUser(user);

            setAuthenticated(
                true
            );

        }
        catch{

            setUser(null);

            setAuthenticated(
                false
            );
        }
    }

    async function signOut(){

        const refresh =
            getRefreshToken();

        if(refresh){

            try{

                await authService.logout(
                    refresh
                );

            }catch{}
        }

        removeTokens();

        setUser(null);

        setAuthenticated(
            false
        );
    }

    useEffect(()=>{

        async function initialize(){

            const token =
                getAccessToken();

            if(token){

                await loadUser();
            }

            setLoading(
                false
            );
        }

        initialize();

    },[]);

    return(

        <AuthContext.Provider
            value={{
                user,
                authenticated,
                loading,
                signIn,
                signOut
            }}
        >

            {children}

        </AuthContext.Provider>

    );
}