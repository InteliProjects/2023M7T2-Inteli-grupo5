import React from 'react';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUser } from "@fortawesome/free-solid-svg-icons";

const Header = () => {
  return (
    <header className="bg-gradient-to-r from-blue-900 via-blue-600 to-blue-700 p-4 text-white text-2xl font-extrabold w-screen">
      <div className="flex items-center justify-between">
        <span className="text-3xl">BleedRunner</span>
        <div className="flex items-center">
          <span className="mr-2"></span>
          <FontAwesomeIcon icon={faUser} className="text-xl" />
        </div>
      </div>
    </header>
  );
};

export default Header;
