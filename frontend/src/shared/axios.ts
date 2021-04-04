import axios from 'axios'

const frontendUrl = process.env.REACT_APP_FRONTEND_URL
const backendUrl = process.env.REACT_APP_BACKEND_URL

const AXIOS = axios.create({
    baseURL: backendUrl,
    headers: {
        'Access-Control-Allow-Origin': frontendUrl,
        'Content-Type': 'application/json',
    },
})

export default AXIOS
