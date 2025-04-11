import { useEffect, useState } from 'react';


type TemporaryBannerProps = {
    message: string;
    duration?: number; // optional, defaults to 10000ms
  };

const Banner = ({ message, duration = 5000 }: TemporaryBannerProps) => {
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => setVisible(false), duration);
    return () => clearTimeout(timer); // cleanup
  }, [duration]);

  if (!visible) return null;

  return (
    <div className="fixed top-4 left-1/2 transform -translate-x-1/2 z-50  text-white px-6 py-3 rounded shadow-lg" style={{"background":"#009933"}}>
      {message}
    </div>
  );
};

export default Banner;