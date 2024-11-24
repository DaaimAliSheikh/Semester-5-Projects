// src/app/auth/login/page.tsx
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore, User } from "@/stores/authStore";
import { useMutation } from "react-query";
import { login } from "@/services/apiService";

const LoginPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  // const { loginMutation } = useAuth();
  const router = useRouter();
  const { setUser, user } = useAuthStore();

  const loginMutation = useMutation({
    mutationFn: login,
    onSuccess: (user) => {
      setUser(user);
    },
    onError: (error) => {
      console.error(error);
    },
  });

  const handleLogin = async () => {
    loginMutation.mutate(
      { email, password },
      {
        onSuccess: (user: User) => {
          user.is_admin ? router.push("/dashboard") : router.push("/");
        },
      }
    );
  };

  return (
    <div>
      <h1>Login {user?.username}</h1>
      <input
        placeholder="Email"
        className=" text-black"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        placeholder="Password"
        type="password"
        value={password}
        className=" text-black"
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleLogin}>Login</button>
    </div>
  );
};

export default LoginPage;
