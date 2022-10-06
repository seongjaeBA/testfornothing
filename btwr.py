import asyncio
from bleak import BleakClient

address = "C4:61:51:AF:3C:E7"
read_write_charcteristic_uuid = "30e649e7-a8a2-46df-b9a8-462aa3470949"

async def run(address):    
    async with BleakClient(address) as client:
        print('connected')
        services = await client.get_services()        
        for service in services:
            for characteristic in service.characteristics:
                if characteristic.uuid == read_write_charcteristic_uuid:                       
                    # 데이터 쓰기전 원래 데이터 읽기
                    if 'read' in characteristic.properties:
                        read_data = await client.read_gatt_char(characteristic)
                        print('read before writing: ', read_data)
                    # 데이터 쓰기
                    if 'write' in characteristic.properties:
                        await client.write_gatt_char(characteristic, bytes(b'7'))                  
                    # 쓰기 이후 데이터 읽기
                    if 'read' in characteristic.properties:
                        read_data = await client.read_gatt_char(characteristic)
                        print('read after writing: ', read_data)
    
    print('disconnect')

loop = asyncio.get_event_loop()
loop.run_until_complete(run(address))
print('done')