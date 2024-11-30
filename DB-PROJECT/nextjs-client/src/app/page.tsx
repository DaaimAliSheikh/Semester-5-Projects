"use client";
import PageLoader from "@/components/PageLoader";
import { useAuthGuard } from "@/hooks/useAuthGuard";

const HomePage = () => {
  const { loading } = useAuthGuard();
  return loading ? (
    <PageLoader />
  ) : (
    <div>
      HomePage
      <div>logout</div>
    </div>
  );
};

export default HomePage;
