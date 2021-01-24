import React, { useState, useEffect } from 'react'

const CardObject = ( card ) => {
  const [smallIMG, setSmallIMG] = useState("")
  const {data} = card;

  const formatted_name = data.name.split(" //")

  useEffect(() => {
      setSmallIMG(data.illustration.small_image)
  },[card, data.illustration.small_image])

  const renderCardPage = () => {
    alert('Card information modal coming soon!');
  }

  return (
    <section className="card-object" onClick={renderCardPage}>
      <h4 style={{ color:"#FFF" }}>{formatted_name[0]}</h4>
      <div className="card-object__image-container">
        {smallIMG ? (
          <img src={smallIMG} alt={data.name + " card image"}/>
        ) : null}
      </div>
    </section>
  )
}

export default CardObject;
