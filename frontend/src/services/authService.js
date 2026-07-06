import api from "../api/axios";

export const login =
    async(data) => {

    const response =
        await api.post(
            "/auth/login",
            data
        );

    return response.data;
};

export const register =
    async(data) => {

    const response =
        await api.post(
            "/auth/register",
            data
        );

    return response.data;
};

export const me =
    async() => {

    const response =
        await api.get(
            "/auth/me"
        );

    return response.data;
};

export const refresh =
    async(refreshToken) => {

    const response =
        await api.post(
            "/auth/refresh",
            {
                refresh_token:
                    refreshToken
            }
        );

    return response.data;
};

export const logout =
    async(refreshToken) => {

    const response =
        await api.post(
            "/auth/logout",
            {
                refresh_token:
                    refreshToken
            }
        );

    return response.data;
};