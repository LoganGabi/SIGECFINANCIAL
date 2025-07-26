document.addEventListener('DOMContentLoaded', function () {

    const id_plannedAccount = document.getElementById("id_plannedAccount");
    if (id_plannedAccount){
        if (id_plannedAccount.checked){
            const date_init = document.getElementById("id_date_init");
            date_init.id = "date_init_planned_account";
            generateInstallmentsPlannedAccount();
        }
        else{
            const date_init = document.getElementById("date_init_planned_account");
            
            if (date_init){
                date_init.id = "id_date_init";
            }
            generateInstallments();
        }
        
    }
    else{
        
        generateInstallments();
    }
   


}
)
function generateInstallmentsPlannedAccount(){
    const header = document.getElementById('installment');
    
    const formContainer = document.getElementById("payment-method-container");

    header.style = 'display:none;'
    //escondendo campos de template base e opção de remoção
    // header.style = 'display:none;'
    const old_payment_method_form = document.getElementById("old-payment-method-form");
    let click = 0 // variavel para verificar quantidade de cliques
    const installments = document.getElementById('generate')//gerador de parcelas
    
    installments.addEventListener('click', () => {
        // Ao clicar em gerar e haver pagamentos presentes no banco, eles serao apagados
        if (old_payment_method_form){                
            old_payment_method_form.style.display="none";
        }

        let TOTAL_FORMS = document.getElementById("id_paymentmethod_accounts_set-TOTAL_FORMS");//TOTAL FORMS
        let mounths_installment_Range = document.getElementById('id_installment_Range');// intervalo em dias entre parcelas
        let installmentRange = document.getElementById('id_numberOfInstallments');//numero de parcela
        let dateInitsemvalor = document.getElementById("date_init_planned_account"); // Data de início das faturas

        if (installmentRange.value <= 0) {
            return 0
        }

        click = click + 1
        console.log('quantidade de cliques ate agora: ' + click)
        if (click > 1){
            if (isNaN(installmentRange) || isNaN(mounths_installment_Range)  || isNaN(startDate) || isNaN(totalValue)) {
                clean(TOTAL_FORMS.value,formContainer)
            }
        }
        
        header.style.removeProperty('display')

        
        const convertToDate = (dateStr) => { //#FIXME inportante
            const [month, year] = dateStr.split('/').map(num => parseInt(num, 10));
            return new Date(year, month - 1); // Mês no JavaScript é baseado em zero
        };
        const inputDate = dateInitsemvalor.value.trim();
        
        // Converter a data inicial
        const startDate = convertToDate(inputDate);
        // Verifica se a data foi convertida corretamente
        if (isNaN(startDate.getTime())) {
            console.error('Data inválida');
            return;
        }

     
        

        const totalValue = parseFloat(document.getElementById("id_totalValue").value); // Valor de cada parcela
        const numberOfInstallments = parseInt(document.getElementById("id_numberOfInstallments").value); // Número de parcelas

        let fragmento = document.createDocumentFragment();
        const valueOfinstallments = compair(numberOfInstallments, totalValue);
        const template = document.getElementById('empty-payment-method-form');
        for (let index = 0; index < installmentRange.value; index++) { 
            let parcela = document.createElement('tr')                  // linha
            parcela.id = `payment-${index + 1}`;
            let row_payment_Method = document.createElement('td')       // coluna
            let row_expirationDate = document.createElement('td')       // coluna
            let row_mounths = document.createElement('td')                 // coluna
            let row_value = document.createElement('td')      
            let row_id = document.createElement("td");                  // coluna                    
            let clone = template.content.cloneNode(true);               // Clonando o template 
            
            
            let counter = 0;
            let counter2 = 0;
            clone.querySelectorAll("input, select").forEach(async (input) => { // interando sobre o formulario
                input.name = input.name.replace("0", index  );
                input.id = input.id.replace("0", index  );
               

                if (input.name.includes("-forma_pagamento")) {
                    row_payment_Method.appendChild(input);
                    parcela.appendChild(row_payment_Method)
                }else if (input.name.includes("-expirationDate")) {
                    // Calcula a data da parcela
                    counter2+=1;
                    let mounth = (parseInt(mounths_installment_Range.value,10));       
                    let newDate = new Date(startDate.getFullYear(), startDate.getMonth() + (counter2*mounth)+1, 0);
                    let final_date = new Date(newDate)
                    input.value = `${final_date.getDate().toString().padStart(2, '0')}/${(final_date.getMonth()+1).toString().padStart(2, '0')}/${final_date.getFullYear()}`  
                    
                    row_expirationDate.appendChild(input)
                    parcela.appendChild(row_expirationDate)
                // CALCULO DE VALOR
                }else if (input.name.includes("-value")) {
                    // Define o valor da parcela
                    input.value = valueOfinstallments[index];
                    row_value.appendChild(input)
                    parcela.appendChild(row_value)
                    
                    //CALCULO DE DIAS
                }else if (input.name.includes("-days")) {
                        // Define os dias entre as parcelas
                        input.value = mounths_installment_Range.value*(index + 1 -counter);

                        counter+=1;
                        row_mounths.appendChild(input)
                        parcela.appendChild(row_mounths)
                            
                }
                else if(input.name.includes("-id")){
                    // input.value = id_payments[0];
                    row_id.appendChild(input);
                    parcela.appendChild(row_id)
                }
               
                await formContainer.appendChild(parcela);
            })
        }    
        TOTAL_FORMS.value = Number(installmentRange.value)
        console.log('total forms é igual a: ' + TOTAL_FORMS.value)
    })
}

function generateInstallments(){
    const credit = document.getElementById("credit");
    let credito_aplicado = false;

    if (credit){  
        const button_credit = document.getElementById("id_apply_credit");
        button_credit.addEventListener("click",()=>{
        if(button_credit.onclick == null){
            if(button_credit.checked){
                credito_aplicado = true;
            }
            else{
                credito_aplicado = false;
            }
        }
        else{
            credito_aplicado = false;
        }
       
    });      
    }

    const header = document.getElementById('installment');
    const formContainer = document.getElementById("payment-method-container");

    header.style = 'display:none;'

   
    //escondendo campos de template base e opção de remoção
    const old_payment_method_form = document.getElementById("old-payment-method-form");
    let click = 0 // variavel para verificar quantidade de cliques
    const installments = document.getElementById('generate')//gerador de parcelas
    
    installments.addEventListener('click', () => {
        // Ao clicar em gerar e haver pagamentos presentes no banco, eles serao apagados
        if (old_payment_method_form){                
            old_payment_method_form.style.display="none";
        }

        const new_form = document.getElementById('new_form');
        new_form.value = 1;
        
        let TOTAL_FORMS = document.getElementById("id_paymentmethod_accounts_set-TOTAL_FORMS");//TOTAL FORMS
        let days_installment_Range = document.getElementById('id_installment_Range');// intervalo em dias entre parcelas
        let installmentRange = document.getElementById('id_numberOfInstallments');//numero de parcela
        let dateInitsemvalor = document.getElementById("id_date_init"); // Data de início das faturas

        click = click + 1;

        if (installmentRange.value <= 0) {
            return 0
        }

        console.log('quantidade de cliques ate agora: ' + click)
        if (click > 1){
            if (isNaN(installmentRange) || isNaN(days_installment_Range)  || isNaN(startDate) || isNaN(totalValue)) {
                clean(TOTAL_FORMS.value,formContainer)
            }
        }
        
        header.style.removeProperty('display')
        const convertToDate = (dateStr) => { //#FIXME inportante
            const [day, month, year] = dateStr.split('/').map(num => parseInt(num, 10));
            return new Date(year, month - 1, day); // Mês no JavaScript é baseado em zero
        };
        const inputDate = dateInitsemvalor.value.trim();
        // Converter a data inicial
        const startDate = convertToDate(inputDate);
        // Verifica se a data foi convertida corretamente
        if (isNaN(startDate.getTime())) {
            console.error('Data inválida');
            return;
        }
        let valor_credito = 0;
        let numberOfInstallments = parseInt(document.getElementById("id_numberOfInstallments").value); // Número de parcelas
        const credit_value = document.getElementById("id_value_apply_credit")

        if(credito_aplicado){
            valor_credito = credit_value.value;
            numberOfInstallments -= 1;
        }
        const totalValue = parseFloat(document.getElementById("id_totalValue").value)-valor_credito;
        // Valor de cada parcela
        const valueOfinstallments = compair(numberOfInstallments, totalValue);
        const template = document.getElementById('empty-payment-method-form');

        let quantInstallments = [
            {
                numeroParcelas:installmentRange.value,
                valorParcelas:valueOfinstallments,
                purpose:'Produto'
            }
        ]

        const id_freightExists = document.getElementById("id_freightExists");
        const id_numberOfInstallmentsFreight = document.getElementById("id_numberOfInstallmentsFreight");
        
        if (id_freightExists){
            const id_freight_type = document.getElementById("id_freight_type");
            const id_valueFreight = document.getElementById("id_valueFreight");
            
            if(
                id_freightExists.checked && 
                id_freight_type.value=="FOB" && 
                id_valueFreight.value > 0 && 
                id_numberOfInstallmentsFreight.value > 0){
                    const valueOfinstallmentsFreight = compair(id_numberOfInstallmentsFreight.value,id_valueFreight.value);
                    quantInstallments.push({
                        numeroParcelas: id_numberOfInstallmentsFreight.value,
                        valorParcelas: valueOfinstallmentsFreight,
                        purpose:'Frete'
                    });
                }
        }

        const id_rmnExists = document.getElementById("id_rmnExists");
        const id_numberOfInstallmentsRMN = document.getElementById("id_numberOfInstallmentsRMN");
        if(id_rmnExists){
            const id_valuePickingList = document.getElementById("id_valuePickingList");
           
            if(id_rmnExists.checked && 
                id_valuePickingList.value > 0 &&
                id_numberOfInstallmentsRMN.value > 0
            ){
                const valueOfinstallmentsRMN = compair(id_numberOfInstallmentsRMN.value,id_valuePickingList.value)
                    quantInstallments.push({
                        numeroParcelas: id_numberOfInstallmentsRMN.value,
                        valorParcelas: valueOfinstallmentsRMN,
                        purpose:'Romaneio'
                    });
            }
        }

        const id_taxExists = document.getElementById("id_taxExists");
        const id_numberOfInstallmentsTax = document.getElementById('id_numberOfInstallmentsTax');
        if(id_taxExists){
            const id_valueTax = document.getElementById("id_valueTax");
           
            if (
                id_taxExists.checked &&
                id_valueTax.value > 0 &&
                id_numberOfInstallmentsTax.value > 0
            ){
                const valueOfinstallmentsTax = compair(id_numberOfInstallmentsTax.value,id_valueTax.value);
                quantInstallments.push({
                    numeroParcelas: id_numberOfInstallmentsTax.value,
                    valorParcelas: valueOfinstallmentsTax,
                    purpose:'Imposto'
                })
            }
        }

        
        let counterId = 0;
        quantInstallments.forEach((item,index)=>{
            for (let index = 0; index < item.numeroParcelas; index++) {     
                let parcela = document.createElement('tr')                  // linha
                parcela.id = `payment-${counterId}`;
                let row_payment_puropose = document.createElement('td')
                let row_payment_Method = document.createElement('td')       // coluna
                let row_expirationDate = document.createElement('td')       // coluna
                let row_days = document.createElement('td')                 // coluna
                let row_value = document.createElement('td')      
                let row_id = document.createElement("td");          // coluna   
                let row_credit = document.createElement("td");      // coluna     
                let clone = template.content.cloneNode(true);               // Clonando o template 

                let counter = 0;
                clone.querySelectorAll("input, select").forEach(async (input) => { // interando sobre o formulario
                    input.name = input.name.replace("0", counterId  );
                    input.id = input.id.replace("0", counterId  );
                
                    if (input.name.includes("-forma_pagamento")) {
                        row_payment_Method.appendChild(input);
                        parcela.appendChild(row_payment_Method);
                        
                    } else if (input.name.includes('-paymentPurpose')){
                        input.value = item.purpose;
                        row_payment_puropose.appendChild(input);
                        parcela.appendChild(row_payment_puropose);
                    }
                    else if (input.name.includes("-expirationDate")) {
                        // Calcula a data da parcela
                        let days = (parseInt(days_installment_Range.value,10))
                        let new_date = startDate.setDate(startDate.getDate() + days);
                        let final_date = new Date(new_date)
                        input.value = `${final_date.getDate().toString().padStart(2, '0')}/${(final_date.getMonth() + 1).toString().padStart(2, '0')}/${final_date.getFullYear()} `  
                        
                        const divExpirationDate  = document.createElement('div');
                        divExpirationDate.className = 'input-group date';
                        divExpirationDate.setAttribute('data-provide','datepicker');
                        divExpirationDate.id= "expiration_date";

                        const inputGroup = document.createElement("div");
                        inputGroup.classList.add("input-group-addon");

                        const span = document.createElement('span');
                        span.className = "glyphicon glyphicon-th";
                        
                        inputGroup.appendChild(span);
                        divExpirationDate.appendChild(input);
                        divExpirationDate.appendChild(inputGroup);

                        row_expirationDate.appendChild(divExpirationDate);
                        parcela.appendChild(row_expirationDate);
                    // CALCULO DE VALOR
                    }else if (input.name.includes("-value")) {
                        // Define o valor da parcela
                        if (index == 0 && credito_aplicado){
                            input.value = credit_value.value;
                        }
                        else if(index !=0 && credito_aplicado){
                            input.value = item.valorParcelas[index-1];
                        }
                        else{
                            input.value = item.valorParcelas[index];
                        }
                        
                        row_value.appendChild(input);
                        parcela.appendChild(row_value);
                        
                    //CALCULO DE DIAS
                    }else if (input.name.includes("-days")) {
                        // Define os dias entre as parcelas
                        input.value = days_installment_Range.value*(counterId + 1 -counter);
                        counter+=1;
                        row_days.appendChild(input)
                        parcela.appendChild(row_days)
                                
                    }
                    else if(input.name.includes("-id")){
                        row_id.appendChild(input);
                        parcela.appendChild(row_id)
                    }
                    else if(input.name.includes("-activeCredit")){
                        if(index == 0 && credito_aplicado){
                            input.checked = true;
                        }
                        row_credit.appendChild(input);
                        parcela.appendChild(row_credit)
                       
                    }
                   
                    await formContainer.appendChild(parcela);
                })
                counterId+=1;
            }   
        })
            
             
        if(id_freightExists && id_rmnExists && id_taxExists){
            let installmentRangeFreightValue = 0;
            let installmentRangeTaxValue = 0;
            let installmentRangeRMNValue = 0;

            if (id_freightExists.checked){
                installmentRangeFreightValue = id_numberOfInstallmentsFreight.value || 0;
            }
            if(id_taxExists.checked){
                installmentRangeTaxValue = id_numberOfInstallmentsTax.value || 0;
            }
            if(id_rmnExists.checked){
                 installmentRangeRMNValue = id_numberOfInstallmentsRMN.value || 0;
            }
           
            
            TOTAL_FORMS.value = Number(installmentRange.value) + Number(installmentRangeFreightValue) + Number(installmentRangeRMNValue) + Number(installmentRangeTaxValue);
            console.log('total forms é igual a: ' + TOTAL_FORMS.value);    
        }
       else{
            TOTAL_FORMS.value = Number(installmentRange.value);
            console.log('total forms é igual a: ' + TOTAL_FORMS.value);    
       }
    })
   
}

export function compair(numero_parcelas, valor_total){
    const array_valor_parcelas = [];
    let all_parcela = 0
    for (let index = 0; index <= numero_parcelas-1; index++) {
        let valor_parcela = (valor_total/numero_parcelas).toFixed(2)
            
        all_parcela = parseFloat(all_parcela) + parseFloat(valor_parcela)
        if(index===numero_parcelas-1){
            let ultima_parcela = parseFloat(valor_parcela) + (valor_total - all_parcela);
            array_valor_parcelas[index] = ultima_parcela.toFixed(2);
        }else {
            array_valor_parcelas[index] = valor_parcela;
        }
    }
    return array_valor_parcelas
    }
export function valida(){
    if (isNaN(numberOfInstallments) || isNaN(installment_Range)  || isNaN(startDate) || isNaN(totalValue)) { 
        alert("Por favor, preencha todos os campos corretamente. BY: kleitin");
        return;
    }
    }
export function clean(total_forms,container){
    for (let index = 0; index < total_forms+1; index++) {
        const del = container.querySelector(`[id$="${index}"]`);
        if (del != null) {
            console.log('variavel del igual a: ' + del.id)
            if(index + 1 >= 1){
                del.remove()
            }
        }
    }
}
    
export function getCSRFToken() {
    let cookieValue = null;
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith('csrftoken=')) {
            cookieValue = cookie.substring('csrftoken='.length, cookie.length);
            break;
        }
    }
    return cookieValue;
}

