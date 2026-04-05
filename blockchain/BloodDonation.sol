// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BloodDonation {
    
    struct DonationRecord {
        string donorId;
        string bloodGroup;
        string donationDate;
        string hospitalName;
        string verificationStatus;
    }

    // Array to store all verified donation records
    DonationRecord[] public records;

    // Event emitted when a new record is added
    event RecordAdded(
        string donorId,
        string bloodGroup,
        string donationDate,
        string hospitalName,
        string verificationStatus
    );

    // Add a new donation record
    function addDonationRecord(
        string memory _donorId,
        string memory _bloodGroup,
        string memory _donationDate,
        string memory _hospitalName,
        string memory _verificationStatus
    ) public {
        records.push(DonationRecord(
            _donorId,
            _bloodGroup,
            _donationDate,
            _hospitalName,
            _verificationStatus
        ));

        emit RecordAdded(
            _donorId,
            _bloodGroup,
            _donationDate,
            _hospitalName,
            _verificationStatus
        );
    }

    // Get total number of records
    function getRecordsCount() public view returns (uint) {
        return records.length;
    }

    // Get a specific record by index
    function getRecord(uint index) public view returns (
        string memory donorId,
        string memory bloodGroup,
        string memory donationDate,
        string memory hospitalName,
        string memory verificationStatus
    ) {
        require(index < records.length, "Index out of bounds");
        DonationRecord memory record = records[index];
        return (
            record.donorId,
            record.bloodGroup,
            record.donationDate,
            record.hospitalName,
            record.verificationStatus
        );
    }
}
