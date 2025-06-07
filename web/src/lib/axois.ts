import axios from "axios";

const createCustomFetch = (version: string) =>
  axios.create({
    baseURL: `${process.env.NEXT_PUBLIC_API_URL}/api/${version}`,
    withCredentials: true,
  });

const customFetch = createCustomFetch("v1");

export { customFetch };
