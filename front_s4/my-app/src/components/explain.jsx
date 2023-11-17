import React from "react";
import Graph from "../public/graph.png";
import Graph_1 from '../public/graph_1.png';
import Image from "next/image";


const Explain = () => {
  return (
    <div className="mt-10 container p-6">
      <h1 className="mb-4 text-4xl font-extrabold leading-none tracking-tight text-gray-900 md:text-5xl lg:text-6xl justify-center flex mt-10">Dados Gerais</h1>
      <div className="md:grid md:grid-cols-2 md:gap-8 gap-4 flex flex-wrap mx-10 my-4">
        
        <div className="grid gap-2">
          <Image src={Graph} alt="foto" className="rounded-lg p-6 shadow-md" />
        </div>
        <div className="grid gap-2 bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-black font-semibold text-4xl">
            Gráfico de Dispersão - f x t
          </h2>
          <p className="text-[1rem] text-gray-600 text-2xl mt-4 leading-relaxed">
            Distribuição histórica do tempo de falha predito pelo modelo, ou seja, qual o número mais apontado pelo modelo.
          </p>
        </div>
      </div>

      <div className="md:grid md:grid-cols-2 md:gap-8 gap-4 flex flex-wrap-reverse mx-10 my-4">
        <div className="grid gap-2 bg-gray-800 p-6 rounded-lg shadow-md">
          <h2 className="text-white font-semibold text-4xl">
            Gráfico de Barras
          </h2>
          <p className="text-[1rem] text-gray-300 text-2xl mt-4 leading-relaxed">
            Esse gráfico tem por prioridade mostrar os aviões específicos que estão mais perto de quebrar, sendo um gráfico de avião x tempo até falha.
          </p>
        </div>
        <div className="grid gap-2">
          <Image src={Graph_1} alt="foto do clube" className="rounded-lg p-6 shadow-md" />
        </div>
      </div>
    </div>
  );
};

export default Explain;
