"use client";
import LogoutButton from "@/components/LogoutButton";
import { useAuthGuard } from "@/hooks/useAuthGuard";

const HomePage = () => {
  const { loading } = useAuthGuard();
  return loading ? (
    "loading"
  ) : (
    <div>
      HomePage
      <div>
        <LogoutButton />
      </div>
    </div>
  );
};

export default HomePage;
