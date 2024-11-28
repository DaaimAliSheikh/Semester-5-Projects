"use client";
import LogoutButton from "@/components/LogoutButton";
import PageLoader from "@/components/PageLoader";
import { useAuthGuard } from "@/hooks/useAuthGuard";

const HomePage = () => {
  const { loading } = useAuthGuard();
  return loading ? (
    <PageLoader />
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
