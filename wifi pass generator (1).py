import subprocess

# The list of networks your Mac Mini just gave us
saved_networks = ["Mim AnzeliT", "L-T,201", "iPhone"]

print("--- Mac Mini Keychain Retrieval ---")

for ssid in saved_networks:
    try:
        # The 'security' command pulls the password for a specific SSID
        # -w means 'only show the password'
        # -a means 'account name' (which is the SSID for Wi-Fi)
        cmd = f"security find-generic-password -wa '{ssid}'"

        # Run the command
        password = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()

        print(f"NETWORK: {ssid:15} | PASSWORD: {password}")

    except subprocess.CalledProcessError:
        # This happens if you click 'Deny' or if the password isn't in the Keychain
        print(f"NETWORK: {ssid:15} | Status: Access Denied or No Password Found")
    except Exception as e:
        print(f"NETWORK: {ssid:15} | Error: {e}")

print("-" * 35)