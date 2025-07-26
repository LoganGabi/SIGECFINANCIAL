// Usando jQuery para facilitar o controle da visibilidade
document.addEventListener('DOMContentLoaded', function () {
    const interestType = document.getElementById('interest_type');
    const fineType = document.getElementById('fine_type');
    const interest = document.getElementById('id_interest');    // juros
    const fine = document.getElementById('id_fine');            // multa
    if (interest.value == ""){
        interest.value = '0.00';
    }
    if (fine.value == ""){
        fine.value = '0.00';
    }

    let TotalValue = document.getElementById('id_value');       // html de valor pago
    let value_edit = TotalValue.value;                          // valor pago
    let ValueOLD = document.getElementById('id_value_old');     // html valor bruto
    //const defalt = ValueOLD.value                               // valor bruto

    // dataa = document.getElementById('id_date_account').value
    data = document.getElementById('id_expirationDate').value
    console.log(data)
    
    const date = document.getElementById("id_date_account") || document.getElementById('id_data_da_venda') || document.getElementById("id_data_da_compra"); // data da conta
    
    const convertToDate = (dateStr) => {
        const [year, month, day ] = dateStr.split('-').map(num => parseInt(num, 10));
        return new Date(year, month - 1, day); // Mês no JavaScript começa do 0
    };
    // Pega o valor do input e remove espaços extras
    const inputDate = date.value.trim();
    // Converte a data inicial para um objeto Date
    const startDate = convertToDate(inputDate);
    if (isNaN(startDate.getTime())) {// Verifica se a conversão foi bem-sucedida
        console.error('Data inválida');
    } else {// Cria uma nova data para evitar modificar startDate
    const final_date = new Date(startDate);

    // Formata a data no formato "DD/MM/YYYY"
    date.value = `${final_date.getDate().toString().padStart(2, '0')}/` +
                 `${(final_date.getMonth() + 1).toString().padStart(2, '0')}/` +
                 `${final_date.getFullYear()}`;
    } 
    fine.addEventListener('change', function(){
        const format = format_value(fine.value)
        if (format === 'NaN'){
            fine.value = '0.00'
        }else fine.value = format
        const edit = compair_interest_fine(ValueOLD.value)
        TotalValue.value = edit
    })

    interest.addEventListener('change', function(){
        const format = format_value(interest.value)
        if (format === 'NaN'){
            interest.value = '0.00'
        }else interest.value = format
        const edit = compair_interest_fine(ValueOLD.value)

        console.log('Este é o edit');
        console.log(edit);
        TotalValue.value = edit;
    })
    
    interestType.addEventListener('change',function() {
        if (interestType.value === 'percent') {
            interest.value = '0.00'
            const edit = compair_interest_fine(ValueOLD.value)
            TotalValue.value = edit
        } else {
            interest.value = '0.00'
            const edit = compair_interest_fine(ValueOLD.value)
            TotalValue.value = edit
        } 
    })

    fineType.addEventListener('change',function() {
        if (fineType.value === 'percent') {
            fine.value = '0.00'
            const edit = compair_interest_fine(ValueOLD.value)
            TotalValue.value = edit
        } else {
            fine.value = '0.00'
            const edit = compair_interest_fine(ValueOLD.value)
            TotalValue.value = edit
        } 
    })

    function format_value(value){

        return parseFloat(value).toFixed(2)
    }


    // #FIXME função para dar o valor total pago 
    function compair_interest_fine(defalt){
        let percent = 0
        let sum = 0
        value_edit = parseFloat(defalt)
        console.log(value_edit)
        console.log('entrou na função de comparação')

        if (interestType.value === 'percent' && (interest.value != '') ){ 
            percent = percent + parseFloat(interest.value)
            if(fineType.value === 'percent' && (fine.value != '') ){
                percent = percent + parseFloat(fine.value)
            }else{  
                if (fine.value != ''){
                    sum = parseFloat(sum) + parseFloat(fine.value)
                }
            }
            value_edit = parseFloat(defalt) + parseFloat((percent/100)*defalt) + parseFloat(sum)
        } else {
            sum = parseFloat(sum) + parseFloat(interest.value)
            if(fineType.value === 'percent' && (fine.value != '' ) ){
                percent = percent + parseFloat(fine.value)
            }else{   
                if (fine.value != ''){   
                    sum = parseFloat(sum) + parseFloat(fine.value)
                }
            }
            value_edit = parseFloat(defalt) + parseFloat((percent/100)*defalt) + sum    
        }
        if (fine.value === ''){     
            fine.value = '0.00'
        }
        if (interest.value === ''){     
            interest.value = '0.00'
        }
        return parseFloat(value_edit).toFixed(2)
    }
})