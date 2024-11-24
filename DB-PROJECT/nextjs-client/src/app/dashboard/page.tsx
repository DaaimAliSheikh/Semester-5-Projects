"use client";

import LogoutButton from "@/components/LogoutButton";
import { useAuthStore } from "@/stores/authStore";

const Dashboard = () => {
  const user = useAuthStore((state) => state.user); ///loaded from localstorage by zustand

  return (
    <div>
      dashboard {user?.user_id}
      <div>
        <LogoutButton />
      </div>
    </div>
  );
};

export default Dashboard;
