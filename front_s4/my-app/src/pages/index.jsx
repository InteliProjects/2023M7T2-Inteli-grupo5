import Explain from "@/components/explain";
import Header from "@/components/header";
import DispersionChart from "../components/dispersionChart";
import DistributionChart from "../components/distribuitionChart";

function Home() {
  return (
    <div>
      <h1 className="mb-4 text-4xl font-bold leading-none tracking-tight text-gray-800 md:text-5xl lg:text-5xl justify-center flex mt-10">Dashboard</h1>
      {/* <Explain /> */}
      <h2 className="mb-4 text-sm font-medium text-gray-500 md:text-lg lg:text-xl justify-center flex mt-10">Tempo de falha por avião</h2>

      <div className="w-full flex flex-col items-center justify-center mb-5">
      <DispersionChart  className="mb-4"/>
      <h2 className="mb-4 text-sm font-medium text-gray-500 md:text-lg lg:text-xl justify-center flex mt-10">Tempos de falha</h2>
      <DistributionChart />
      </div>
    </div>
  );
}
export default Home;
