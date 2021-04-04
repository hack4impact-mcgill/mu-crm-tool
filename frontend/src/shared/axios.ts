import axios from 'axios'

const frontendUrl = 'http://localhost:3000'
const backendUrl = 'http://localhost:5000'

const AXIOS = axios.create({
    baseURL: backendUrl,
    headers: {
        'Access-Control-Allow-Origin': frontendUrl,
        'Content-Type': 'application/json',
    },
})

export default AXIOS
