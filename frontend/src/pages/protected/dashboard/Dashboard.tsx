// Main Dashboard page after successfull login
import React from 'react'
import { Map } from '@/components/MapView/Map'

interface prop {
  className?: string
};

const Dashboard = ({ className = '' }: prop) => {
  console.log("Dashboard: ", className);
  return (
    <div className={` ${className}`}>
      <Map  className={` ${className}`}/>
    </div>
  )
}

export default Dashboard
