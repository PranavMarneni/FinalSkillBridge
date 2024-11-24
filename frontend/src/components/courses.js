import React from 'react';
import './courses.css'; // Import the CSS for styling

const courses = [
  { id: 1, image: 'https://link-to-image1.com', url: 'https://course1.com' },
  { id: 2, image: 'https://link-to-image2.com', url: 'https://course2.com' },
  { id: 3, image: 'https://link-to-image3.com', url: 'https://course3.com' },
  // Add more courses as needed
];

const CourseSlider = () => {
  return (
    <div className="course-slider">
      <div className="slider-container">
        {courses.map((course) => (
          <div className="slide" key={course.id}>
            <a href={course.url} target="_blank" rel="noopener noreferrer">
              <img src={course.image} alt={`Course ${course.id}`} className="course-image" />
            </a>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CourseSlider;
