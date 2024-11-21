import React, { useState } from "react";
import logo from "../../../resource/logo.png";
import { NavLink, useNavigate } from "react-router-dom";
import { postData } from "api/api-method";
const Signin = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState("");
  const [pw, setPw] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    const formData = new URLSearchParams();
    formData.append("username", "admintest123@gmail.com");
    // formData.append("password", "1212312121");
    // formData.append("username", "leadresearchertest123@gmail.com");
    formData.append("password", "1212312121");
    console.log(formData);
    try {
      const response = await postData(
        "http://127.0.0.1:8000/token",

        {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        formData.toString()
      );
      if (response?.access_token) {
        localStorage.setItem("token", response.access_token);
        navigate("/admin");
      }
      console.log("Request submitted successfully:", response.access_token);
      console.log(response);
    } catch (error) {
      console.error("Error submitting request:", error);
    }
  };
  return (
    <section className="bg-gray-1 py-20 dark:bg-dark lg:py-[120px]">
      <div className="container mx-auto">
        <div className="-mx-4 flex flex-wrap">
          <div className="w-full px-4">
            <div className="relative mx-auto max-w-[525px] overflow-hidden rounded-lg bg-white px-10 py-16 text-center dark:bg-dark-2 sm:px-12 md:px-[60px]">
              <div className="mb-10 text-center md:mb-16">
                <NavLink to="/">
                  <img
                    loading="lazy"
                    src={logo}
                    className="mx-auto inline-block max-w-[160px]"
                    alt="Company logo"
                  />
                </NavLink>
              </div>
              <form onSubmit={handleSubmit}>
                <InputBox
                  type="email"
                  name="email"
                  placeholder="Email"
                  value={user}
                  onChange={(e) => setUser(e.target.value)}
                  required
                />
                <InputBox
                  type="password"
                  name="password"
                  placeholder="Password"
                  value={pw}
                  onChange={(e) => setPw(e.target.value)}
                  required
                />
                <div className="mb-10">
                  <input
                    type="submit"
                    value={isLoading ? "Loading..." : "Sign In"}
                    disabled={isLoading}
                    className={`py-2 px-3 rounded-full border-2 ${
                      isLoading
                        ? "bg-black text-white cursor-not-allowed"
                        : "border-black hover:bg-black hover:text-white"
                    } transition-all duration-300 ease-in-out cursor-pointer`}
                  />
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Signin;

const InputBox = ({ type, placeholder, name }) => {
  return (
    <div className="mb-6">
      <input
        type={type}
        placeholder={placeholder}
        name={name}
        className="w-full rounded-md border border-stroke bg-transparent px-5 py-3 text-base text-body-color outline-none focus:border-primary focus-visible:shadow-none dark:border-dark-3 dark:text-black hover:outline-2 hover:outline-black transition-all duration-300 ease-in-out"
        style={{ boxSizing: "border-box" }}
      />
    </div>
  );
};
