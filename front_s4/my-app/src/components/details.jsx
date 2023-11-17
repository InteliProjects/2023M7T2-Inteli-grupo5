import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPlane } from "@fortawesome/free-solid-svg-icons";

const Details = () => {
  return (
    <div className="mt-6 container mx-10">
      <div className="md:grid md:grid-cols-2 md:gap-8 gap-4 flex flex-wrap my-4">
        <div className="grid gap-2 bg-white p-6 rounded-lg shadow-md">
        <FontAwesomeIcon icon={faPlane} className="text-blue-500 text-3xl" />
          <p className="text-[1rem] text-gray-600 text-2xl mt-4 leading-relaxed">
            18290-0 Avião Embraer
          </p>
        </div>
        <div className="grid gap-2 bg-white p-6 rounded-lg shadow-md">
        <FontAwesomeIcon icon={faPlane} className="text-blue-500 text-3xl" />
          <p className="text-[1rem] text-gray-600 text-2xl mt-4 leading-relaxed">
             18290-0 Avião Embraer
          </p>
        </div>
      </div>

        <div className="md:grid md:grid-cols-2 md:gap-8 gap-4 flex flex-wrap my-4">
         <div className="grid gap-2 bg-white p-6 rounded-lg shadow-md">
         <FontAwesomeIcon icon={faPlane} className="text-blue-500 text-3xl" />
          <p className="text-[1rem] text-gray-600 text-2xl mt-4 leading-relaxed">
          18290-0 Avião Embraer
          </p>
        </div>
        <div className="grid gap-2 bg-white p-6 rounded-lg shadow-md">
        <FontAwesomeIcon icon={faPlane} className="text-blue-500 text-3xl" />
          <p className="text-[1rem] text-gray-600 text-2xl mt-4 leading-relaxed">
          18290-0 Avião Embraer
          </p>
        </div>
      </div>
    </div>
  );
};

export default Details;
