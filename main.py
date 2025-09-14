def encrypt(plaintext, key="SAY"):
    """
    使用多层加密算法生成设备激活码
    
    Args:
        plaintext (str): 要加密的设备ID
        key (str): 加密密钥，默认为"SAY"
    
    Returns:
        str: 加密后的十六进制激活码
    
    Raises:
        ValueError: 当输入参数无效时
    """
    if not plaintext or not isinstance(plaintext, str):
        raise ValueError("设备ID不能为空且必须是字符串")
    
    if not key or not isinstance(key, str):
        raise ValueError("密钥不能为空且必须是字符串")
    
    try:
        shift_bits = sum(ord(c) for c in key) % 7 + 1
        xor_keys = key.encode()
        block_size = max(1, len(key))
        
        shifted = bytes((b >> shift_bits) | ((b << (8 - shift_bits)) & 0xFF) 
                      for b in plaintext.encode())
        
        xored = bytes(b ^ xor_keys[i % len(xor_keys)] for i, b in enumerate(shifted))
        
        padding = block_size - (len(xored) % block_size)
        padded = xored + bytes([padding] * padding)
        blocks = [padded[i:i+block_size] for i in range(0, len(padded), block_size)]
        reversed_blocks = b"".join(block[::-1] for block in blocks)
        
        return reversed_blocks.hex().upper()
    
    except Exception as e:
        raise ValueError(f"加密过程中发生错误: {str(e)}")


def main():
    """主程序入口"""
    try:
        device_id = input("请输入设备ID: ").strip()
        
        if not device_id:
            print("错误: 设备ID不能为空")
            return
        
        activation_code = encrypt(device_id)
        print(f"激活码: {activation_code}")
        
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"错误: {str(e)}")


if __name__ == "__main__":
    main()
