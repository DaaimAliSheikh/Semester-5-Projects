import { logout } from "@/services/apiService";
import { useAuthStore } from "@/stores/authStore";
import { useRouter } from "next/navigation";
import React from "react";
import { useMutation } from "react-query";

const LogoutButton = () => {
  const setUser = useAuthStore((state) => state.setUser);
  const router = useRouter();
  const logoutMutation = useMutation({
    mutationFn: logout,
    onSuccess: () => {
      setUser(null);
      router.push("/auth/login");
    },
    onError: (error) => {
      console.error(error);
    },
  });
  return <button onClick={() => logoutMutation.mutate()}>LogoutButton</button>;
};

export default LogoutButton;
