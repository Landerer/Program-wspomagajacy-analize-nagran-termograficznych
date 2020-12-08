function sprawdzAnkiete(attribute)
{
    komunikat = "";
    if (isNaN(document.querySelector('input[name="id"]').valueAsNumber)) 
    {
        komunikat += "Podaj prawidłowo numer identyfikacyjny!\n";
    }
    
    if (document.querySelector('input[name="objawy"]:checked') == null) 
    {
        komunikat += "Podaj czy masz objawy Covid19!\n";
    }
    
    if (document.querySelector('input[name="kontaktCovid"]:checked') == null) 
    {
        komunikat += "Podaj czy miałeś kontakt z chorym na Covid19!\n";
    }
    
    if (document.querySelector('input[name="zagranica"]:checked') == null) 
    {
        komunikat += "Podaj czy przebywałeś za granicą!\n";
    }
    
    if (isNaN(document.querySelector('input[name="telefon"]').valueAsNumber)) 
    {
        komunikat += "Podaj prawidłowo numer telefonu!\n";
    }
    
    if (document.querySelector('input[name="plec"]:checked') == null) 
    {
        komunikat += "Podaj płeć!\n";
    }
    
    if (isNaN(document.querySelector('input[name="wiek"]').valueAsNumber)) 
    {
        komunikat += "Podaj prawidłowo wiek!\n";
    }
    
    if (document.querySelector('input[name="wojewodztwo"]:checked') == null) 
    {
        komunikat += "Podaj województwo zamieszkania!\n";
    }
    
    if (document.querySelector('input[name="wielkoscMiejscaZamieszkania"]:checked') == null) 
    {
        komunikat += "Podaj wielkoć miejsca zamieszkania!\n";
    }
    
    if (document.querySelector('input[name="marzniecie"]:checked') == null) 
    {
        komunikat += "Podaj jak często marzną ci dłonie i stopy!\n";
    }
    
    if (document.querySelector('input[name="sinienie"]:checked') == null) 
    {
        komunikat += "Podaj jak często sinieją/bieleją ci dłonie i stopy!\n";
    }
    
    if (document.querySelector('input[name="zimneKapiele"]:checked') == null) 
    {
        komunikat += "Podaj jak często kąpiesz się w zimnej wodzie!\n";
    }
    
    if (document.querySelector('input[name="morsowanie"]:checked') == null) 
    {
        komunikat += "Podaj jak często morsujesz!\n";
    }
    
    if (document.querySelector('input[name="unikanieZimna"]:checked') == null) 
    {
        komunikat += "Podaj czy zalecono ci unikanie ekspozycji na zimno!\n";
    }
    
    if (komunikat) {
        alert(komunikat);
        event.preventDefault();
    }
}