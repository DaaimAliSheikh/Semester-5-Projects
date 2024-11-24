// src/app/auth/signup/page.tsx
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore, User } from "@/stores/authStore";
import { useMutation } from "react-query";
import { signUp } from "@/services/apiService";

const SignUpPage = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();
  const setUser = useAuthStore((state) => state.setUser);

  const signupMutation = useMutation({
    mutationFn: signUp,
    onSuccess: (user) => {
      setUser(user);
    },
    onError: (error) => {
      console.error(error);
    },
  });

  const handleSignUp = async () => {
    signupMutation.mutate(
      { username, email, password },
      {
        onSuccess: (user: User) => {
          user.is_admin ? router.push("/dashboard") : router.push("/");
        },
      }
    );
  };

  return (
    <div>
      <h1>Sign Up</h1>
      <input
        placeholder="Username"
        className="text-black"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        placeholder="Email"
        className="text-black"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        placeholder="Password"
        className="text-black"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleSignUp}>Sign Up</button>
    </div>
  );
};

export default SignUpPage;
