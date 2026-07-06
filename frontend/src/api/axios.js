import axios from "axios";

import {
    getAccessToken,
    getRefreshToken,
    setAccessToken,
    removeTokens
} from "../services/tokenService";

const api = axios.create({
    baseURL:
        "http://127.0.0.1:8000"
});

api.interceptors.request.use(

    config => {

        const token =
            getAccessToken();

        if(token){

            config.headers.Authorization =
                `Bearer ${token}`;
        }

        return config;
    }
);

api.interceptors.response.use(

    response => response,

    async error => {

        const original =
            error.config;

        if(
            error.response?.status === 401 &&
            !original._retry
        ){

            original._retry = true;

            try{

                const refresh =
                    getRefreshToken();

                const response =
                    await axios.post(

                        "http://127.0.0.1:8000/auth/refresh",

                        {
                            refresh_token:
                                refresh
                        }
                    );

                const newToken =
                    response.data
                        .access_token;

                setAccessToken(
                    newToken
                );

                original.headers.Authorization =
                    `Bearer ${newToken}`;

                return api(
                    original
                );

            }
            catch{

                removeTokens();

                window.location.href =
                    "/login";
            }
        }

        return Promise.reject(
            error
        );
    }
);

export default api;