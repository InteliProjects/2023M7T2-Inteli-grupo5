import "../styles/globals.css";
import Head from "next/head";
import Sidebar from "@/components/sidebar";
import { useRouter } from "next/router";

function MyApp({ Component, pageProps }) {
  const router = useRouter();
  const path = router.pathname;

  if ((path === "/login") | (path === "/signup"))
    return <Component {...pageProps} />;

  return (
    <div className="flex w-screen">
      <Head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      </Head>

      <div className="w-1/5 bg-gray-200 h-full">
        <Sidebar />
      </div>

      <div className="w-3/4">
        {" "}
        {/* Main Content */}
        <Component {...pageProps} />
      </div>
    </div>
  );
}

export default MyApp;
