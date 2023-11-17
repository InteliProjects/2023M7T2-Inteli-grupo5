import React from "react";
import Image from "next/image";
import { useRouter } from "next/router";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faChartBar, faUpload, faPlane, faSignOut } from "@fortawesome/free-solid-svg-icons";
import azul from '../public/icon_azul.png'

const Sidebar = () => {
  const router = useRouter();

  const isLinkActive = (path) => {
    return router.pathname === path
      ? "bg-blue-700 text-white border-b-4 border-blue-600"
      : "hover:bg-blue-700";
  };

  return (
    <div className="fixed bg-blue-900 w-1/5 h-screen flex flex-col items-center justify-between p-4 text-white">
      <Image src={azul} alt="azul icon" className="w-10 mt-2" />
      <ul className="space-y-4 mb-52">
        <li>
          <a href="/" className={`flex items-center px-2 py-1 rounded-md ${isLinkActive("/")}`}>
            <FontAwesomeIcon icon={faChartBar} className="mr-2" />
            Dashboard
          </a>
        </li>
        <li>
          <a
            href="/upload"
            className={`flex items-center px-2 py-1 rounded-md ${isLinkActive("/upload")}`}
          >
            <FontAwesomeIcon icon={faUpload} className="mr-2" />
            Upload  
          </a>
        </li>
        <li>
          <a
            href="/planes"
            className={`flex items-center px-2 py-1 rounded-md ${isLinkActive("/planes")}`}
          >
            <FontAwesomeIcon icon={faPlane} className="mr-2" />
            Planes
          </a>
        </li>
        <li className="mt-auto">
          <a
            href="/signout"
            className={`flex items-center px-2 py-1 rounded-md ${isLinkActive("/signout")}`}
          >
            <FontAwesomeIcon icon={faSignOut} className="mr-2" />
            Logout
          </a>
        </li>
      </ul>
    </div>
  );
};

export default Sidebar;
