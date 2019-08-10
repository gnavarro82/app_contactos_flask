//Seleccionar todos los botones
const btneliminar = document.querySelectorAll('.btn-eliminar'); //devuelve lista de nodos html
//comrobar si existen los botones
if(btneliminar){
	//se pasa a un arreglo la lista 
	const btnarray = Array.from(btneliminar);
	//recorrer el array ---
	//por cada boton  que se recore, se agregara un evento de escucha
	btneliminar.forEach((btn) =>{
		btn.addEventListener('click', (e) => {
			if(!confirm('Estas seguro de querer eliminarlo?')){
				//cancelar el evento click
				e.preventDefault();
			}
		});
	});
}