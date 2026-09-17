// Main home/landing page
import React from 'react'
import Dashboard from '../protected/dashboard/Dashboard'

interface prop {
    className?: string
};

const HomePage = ({ className = '' }: prop) => {
    console.log("Home Page: ", className);

    return (
        <div>
            <Dashboard className={` ${className}`} />
        </div>
    );
}

export default HomePage;
